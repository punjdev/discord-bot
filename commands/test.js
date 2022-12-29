module.exports = {
    name: 'test',
    description: 'This is the test command',
    execute(message, args){
        message.channel.send('test');

    }
}