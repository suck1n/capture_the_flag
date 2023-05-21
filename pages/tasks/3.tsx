import React, {Component} from "react";
import Task from "../../components/Task";

export default class CookieReplay extends Component<any, any> {

    constructor(props) {
        super(props);
    }

    render() {

        return (
            <Task title={"Fallmerayer Lottery"} id={3} file_names={"lottery.zip"}>
                <p>Du hast genau so wie wir nie Glück bei den Lottoziehungen? Dich nervt es ebenfalls jede Woche auf die Lottoziehungen zu warten? Probiere es mal mit <em>Fallmerayer Lottery</em>! Hier kannst Du deinen Lottoschein direkt einlösen und bekommst sofort das Ergebnis der neuesten Ziehung!</p>
                <p>Um kryptographisch sichere Lottozahlen zu generieren benutzt <em>Fallmerayer Lottery</em> eine CSPRNG Konstruktion: AES im Counter Modus mit zufälligem Schlüssel und Nonce (Number used Once).</p>
                <p>Um bei jedem Spieler verschiedene Lottoziehungen zu haben, wird der Seed für die Random Zahlen im Cookie abgespeichert!</p>
                <p>Aber wir wollen natürlich kein Glücksspiel promoten, also gibt es eventuell eine klevere Möglichkeit doch die Zahlen der nächsten Ziehung vorherzusagen...</p>
            </Task>
        );
    }
}
