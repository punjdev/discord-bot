module.exports = {
    name: 'channeltest',
    description: 'checking if the channel is correct',
    execute(message, args){
        const channelname = message.channel.id;
        message.channel.send(channelname);

    }
}