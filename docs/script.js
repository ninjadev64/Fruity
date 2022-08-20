var helpTextDiv = document.getElementById("helpText");

function updateEmbed(value) {
    helpTextDiv.innerHTML = null;
    let category = null;
    switch (value) {
        case "fun": category = fun; break;
        case "minigames": category = minigames; break;
        case "points": category = points; break;
        case "other": category = other; break;
        default: category = fun; break;
    }
    category.forEach(command => {
        let div = document.createElement("div");
        
        let title = document.createElement("b");
        title.innerText = command.command;
        
        let description = document.createElement("p");
        description.innerText = command.description;

        div.appendChild(title);
        div.appendChild(description);
        div.appendChild(document.createElement("br"));
        helpTextDiv.appendChild(div);
    });
}
updateEmbed("fun");