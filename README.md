# LeetCode Discord Bot

A Discord bot that helps track LeetCode questions per server. Users can add, list, and delete questions from a shared list.

## Features

- **Add Questions**: `!addq <question1> <question2> ...` - Add one or more questions to the server's list
- **List Questions**: `!listq` - Display all questions for the current server
- **Delete Questions**: `!delq <id>` - Delete a question by its ID (requires manage messages permission)

## Local Development Setup

1. **Clone the repository**
   ```bash
   git clone <your-repo-url>
   cd leetcode-bot
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up environment variables**
   - Copy `env.example` to `.env`
   - Add your Discord bot token to the `.env` file
   ```bash
   cp env.example .env
   # Edit .env and add your DISCORD_TOKEN
   ```

4. **Run the bot**
   ```bash
   python leetcode_bot.py
   ```

## Railway Deployment (Recommended)

Railway makes deployment super easy with automatic containerization and PostgreSQL database.

### Prerequisites
- Railway account (free tier available)
- Discord bot token

### Deployment Steps

1. **Connect your repository to Railway**
   - Go to [Railway Dashboard](https://railway.app/)
   - Click "New Project" → "Deploy from GitHub repo"
   - Connect your GitHub repository

2. **Add PostgreSQL Database**
   - In your Railway project, click "New" → "Database" → "PostgreSQL"
   - Railway will automatically provide a `DATABASE_URL` environment variable

3. **Set Environment Variables**
   - Go to your project's "Variables" tab
   - Add `DISCORD_TOKEN` with your Discord bot token
   - The `DATABASE_URL` will be automatically set by Railway

4. **Deploy**
   - Railway will automatically detect your Python app
   - It will install dependencies from `requirements.txt`
   - Your bot will be deployed and running!

### Railway-Specific Files

- **`requirements.txt`**: Python dependencies
- **`Procfile`**: Tells Railway how to run your app
- **`.env.example`**: Template for environment variables
- **`.gitignore`**: Prevents sensitive files from being committed

## Discord Bot Setup

1. **Create a Discord Application**
   - Go to [Discord Developer Portal](https://discord.com/developers/applications)
   - Click "New Application"
   - Give it a name (e.g., "LeetCode Bot")

2. **Create a Bot**
   - Go to the "Bot" section
   - Click "Add Bot"
   - Copy the token (this is your `DISCORD_TOKEN`)

3. **Set Bot Permissions**
   - Go to "OAuth2" → "URL Generator"
   - Select scopes: `bot`, `applications.commands`
   - Select permissions: `Send Messages`, `Read Message History`, `Manage Messages`
   - Use the generated URL to invite the bot to your server

4. **Configure Intents**
   - In the Bot section, enable "Message Content Intent"
   - This is required for the bot to read command messages

## Environment Variables

| Variable | Description | Required | Source |
|----------|-------------|----------|---------|
| `DISCORD_TOKEN` | Your Discord bot token | Yes | Manual setup |
| `DATABASE_URL` | PostgreSQL connection string | Yes | Railway auto-provided |

## Database

The bot uses SQLite locally and PostgreSQL on Railway:
- **Local Development**: SQLite (`question_tracker.db`)
- **Production (Railway)**: PostgreSQL (automatically provided)

## Monitoring and Logs

- **Railway logs**: View in Railway dashboard under your project
- **Application logs**: Check the console output for INFO/ERROR messages
- **Database**: Monitor in Railway dashboard under the PostgreSQL service

## Security Considerations

1. **Never commit your `.env` file** (already in .gitignore)
2. **Use environment variables** for sensitive data
3. **Regularly rotate your Discord bot token**
4. **Monitor bot permissions** - only grant necessary permissions
5. **Railway handles database backups** automatically

## Troubleshooting

### Common Issues

1. **Bot not responding**: Check if the token is correct and bot is online
2. **Permission errors**: Ensure bot has proper permissions in Discord server
3. **Database connection errors**: Check Railway's PostgreSQL service status
4. **Deployment failures**: Check Railway logs for dependency or environment issues

### Logs to Check

- **Railway logs**: Project dashboard → "Deployments" → "View Logs"
- **Discord API**: Check bot status in Discord Developer Portal
- **Database**: Railway dashboard → PostgreSQL service → "Connect" tab

## Updates and Maintenance

1. **Push changes to GitHub**: Railway automatically redeploys
2. **Monitor Railway dashboard**: Check deployment status and logs
3. **Scale if needed**: Railway allows easy scaling in the dashboard

## Alternative Deployments

### VPS/Cloud Server

If you prefer traditional server deployment:

1. **SSH into your server**
2. **Clone the repository**
3. **Install Python dependencies**
4. **Set up environment variables**
5. **Create a systemd service** for auto-restart
6. **Use PostgreSQL or keep SQLite for single instance**

### Docker Deployment

If you want containerized deployment elsewhere:

1. **Create a Dockerfile**
2. **Use docker-compose.yml**
3. **Set environment variables**
4. **Deploy with `docker-compose up -d`**

## Support

For issues or questions:
1. Check Railway logs for deployment errors
2. Verify your Discord bot setup
3. Ensure all environment variables are set correctly
4. Check Railway's documentation for platform-specific issues 