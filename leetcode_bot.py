# leetcode_bot.py

import discord
from discord.ext import commands
import sqlite3
import os
from dotenv import load_dotenv
import logging
from datetime import datetime
import asyncio

# Set up basic logging
logging.basicConfig(level=logging.INFO)

# Load environment variables from .env file
load_dotenv()
DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")

# --- Bot Setup ---
# Define the intents your bot needs.
intents = discord.Intents.default()
intents.messages = True
intents.message_content = True
intents.guilds = True

bot = commands.Bot(command_prefix="!", intents=intents)

# --- Database Setup ---
DB_FILE = "question_tracker.db"

def initialize_database():
    """Initializes the SQLite database and creates the questions table if it doesn't exist."""
    try:
        conn = sqlite3.connect(DB_FILE)
        cursor = conn.cursor()
        # For tracking assigned questions per server
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS questions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                guild_id INTEGER NOT NULL,
                name TEXT NOT NULL,
                added_by_name TEXT NOT NULL,
                date_added TEXT NOT NULL,
                UNIQUE(guild_id, name)
            )
        """)
        conn.commit()
        conn.close()
        logging.info("Database initialized successfully.")
    except sqlite3.Error as e:
        logging.error(f"Database error on initialization: {e}")


# --- Bot Events ---
@bot.event
async def on_ready():
    """Event handler for when the bot is ready."""
    logging.info(f"Logged in as {bot.user.name} ({bot.user.id})")
    initialize_database()

@bot.event
async def on_command_error(ctx, error):
    """Basic error handling."""
    if isinstance(error, commands.CommandNotFound):
        return
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send("❌ You are missing a required argument for this command. Usage: `!addq <question1> [question2] ...`")
    else:
        logging.error(f"An unhandled error occurred: {error}")
        await ctx.send("An unexpected error occurred. Please check the logs.")


# --- Question Tracker Commands ---

@bot.command(name="addq", help="Adds one or more questions to the list. Usage: !addq <q1> <q2> ...")
async def add_question(ctx, *questions: str):
    """Adds one or more questions to the server's tracked list."""
    if not questions:
        await ctx.send("❌ You need to provide at least one question name or number.")
        return

    guild_id = ctx.guild.id
    added_by_name = ctx.author.display_name
    date_added = datetime.utcnow().strftime("%Y-%m-%d")
    
    added_questions = []
    duplicate_questions = []

    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()

    for name in questions:
        try:
            cursor.execute("INSERT INTO questions (guild_id, name, added_by_name, date_added) VALUES (?, ?, ?, ?)",
                           (guild_id, name, added_by_name, date_added))
            added_questions.append(name)
        except sqlite3.IntegrityError:
            duplicate_questions.append(name)
        except sqlite3.Error as e:
            logging.error(f"DB error in add_question loop: {e}")
            await ctx.send(f"❌ A database error occurred while trying to add '{name}'.")
            continue # Move to the next question

    conn.commit()
    conn.close()

    # Create a summary response
    response_message = ""
    if added_questions:
        response_message += f"✅ **Added:** {', '.join(added_questions)}\n"
    if duplicate_questions:
        response_message += f"⚠️ **Already exist:** {', '.join(duplicate_questions)}"
    
    if response_message:
        await ctx.send(response_message)


@bot.command(name="listq", help="Lists all assigned questions.")
async def list_questions(ctx):
    """Lists all questions for the server."""
    guild_id = ctx.guild.id
    try:
        conn = sqlite3.connect(DB_FILE)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        cursor.execute("SELECT id, name, added_by_name, date_added FROM questions WHERE guild_id = ? ORDER BY id", (guild_id,))
        questions = cursor.fetchall()
        conn.close()

        if not questions:
            await ctx.send("No questions have been added yet. Use `!addq <name>` to add one.")
            return

        embed = discord.Embed(title=f"📚 Assigned Questions for {ctx.guild.name}", color=discord.Color.blue())
        
        description = []
        for q in questions:
            description.append(f"`#{q['id']}`: **{q['name']}** (Added by {q['added_by_name']} on {q['date_added']})")
        
        embed.description = "\n".join(description)
        await ctx.send(embed=embed)

    except sqlite3.Error as e:
        await ctx.send("❌ A database error occurred.")
        logging.error(f"DB error in list_questions: {e}")
        
@bot.command(name="delq", help="Deletes a question from the list. Usage: !delq <Question ID>")
@commands.has_permissions(manage_messages=True) # Only users who can manage messages can delete
async def delete_question(ctx, question_id: int):
    """Deletes a question from the server's list."""
    guild_id = ctx.guild.id
    try:
        conn = sqlite3.connect(DB_FILE)
        cursor = conn.cursor()
        
        # Check if the question exists before deleting
        cursor.execute("SELECT name FROM questions WHERE id = ? AND guild_id = ?", (question_id, guild_id))
        question = cursor.fetchone()
        
        if not question:
            await ctx.send(f"❌ Question with ID `#{question_id}` not found.")
            conn.close()
            return
            
        cursor.execute("DELETE FROM questions WHERE id = ? AND guild_id = ?", (question_id, guild_id))
        conn.commit()
        conn.close()
        
        await ctx.send(f"🗑️ Question `#{question_id}: {question[0]}` has been deleted.")
        
    except sqlite3.Error as e:
        await ctx.send("❌ A database error occurred.")
        logging.error(f"DB error in delete_question: {e}")

@delete_question.error
async def delete_question_error(ctx, error):
    if isinstance(error, commands.CheckFailure):
        await ctx.send("🚫 You don't have permission to delete questions.")


# --- Run the Bot ---
async def main():
    """The main function to start the bot."""
    if not DISCORD_TOKEN:
        logging.error("DISCORD_TOKEN not found in .env file. Please set it up.")
        return
        
    async with bot:
        await bot.start(DISCORD_TOKEN)

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logging.info("Bot is shutting down.")
