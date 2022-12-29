const Discord = require('discord.js');
const client = new Discord.Client({ intents: ["GUILDS", "GUILD_MESSAGES"] });
const prefix = '>';
const fs = require('fs');
client.commands = new Discord.Collection();

const commandFile = fs.readdirSync('./commands/').filter(file => file.endsWith('.js'));

for(const file of commandFile){
    const command = require(`./commands/${file}`);
    client.commands.set(command.name, command);
}

client.once('ready', () => {
    console.log('Mason Plumber is ready!');
});

// const userId = message.guild.members.find(m => m.id === "USER ID HERE");

client.on('message', message =>{
    // mesage starts with the prefix
    temp = message.content
    if(!temp.indexOf(prefix) === 0 || message.author.bot) return;    
    const args = message.content.slice(prefix.length).split(/ +/);
    const command = args.shift().toLowerCase();
    // const command = message.content.slice(0);

    console.log(command + 'tt')

    if(command === 'test'){
        message.channel.send('pre');
        client.commands.get('test.js').execute(message, args);
    }
});

client.login('ODMzNDUyODAzNjE5Njg0NDAx.GLB6Rx.6mBkzDkpSMct91yIiF1AeFgiBDGgp6M4NUrDrM');
