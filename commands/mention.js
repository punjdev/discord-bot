module.exports = {
    name: 'mention',
    description: 'mentioning',
    execute(message, args){
        const userId = message.guild.members.find(m => m.id === "USER ID HERE");
        message.channel.send(userId);

    }
}