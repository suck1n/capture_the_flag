import React, {Component} from "react";
import Task from "../../components/Task";

export default class SQLInjection extends Component<any, any> {

    constructor(props) {
        super(props);
    }

    render() {

        return (
            <Task title={"Capture-The-Flag"} id={0}>
                <p>CTF oder auch Capture-The-Flag ist ein Spiel, in welchem es darum geht eine Flagge zu suchen und diese "einzunehmen".</p>
                <p>Flaggen erhältst du, indem du bestimmte Sicherheitslücken eines Systems findest und ausnutzt um die Flagge zu bekommen.</p>
                <p>Eine Flagge sieht so aus: <i><strong>flag&#123;xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx&#125;</strong></i><br/>Ein 'x' könnte dabei entweder ein Buchstabe oder eine Zahl sein.</p>
                <p>Sobald du eine Flagge gefunden hast, kannst du sie auf der Scoreboard Seite ganz oben einlösen und somit deinen Platz auf dem Scoreboard sichern.</p>
                <p>Deine erste Flagge ist auf der Seite unten versteckt (diese wird jedoch noch nicht für das Scoreboard zählen). Viel Glück!</p>
                <p><strong>Hinweis:</strong> Den Source Code einer Webseite kannst du über <i>Strg + U</i> oder <i>Rechtsklick {">"} Seitenquelltext anzeigen</i> ansehen!</p>
            </Task>
        );
    }
}
