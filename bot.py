@bot.command()
@commands.is_owner()
async def clear_guild(ctx):
    # Target the current guild
    guild = ctx.guild 
    # Clear local cache for this specific guild
    bot.tree.clear_commands(guild=guild)
    # Sync the empty list back to this guild
    await bot.tree.sync(guild=guild)
    await ctx.send(f"All slash commands for {guild.name} have been deleted.")
