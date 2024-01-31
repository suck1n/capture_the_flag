import React, {Component} from "react";
import Task from "../../components/Task";

export default class PaddingOracle extends Component<any, any> {

    constructor(props) {
        super(props);
    }

    render() {

        return (
            <Task title={"Padding Oracle"} id={10} path={":5010"} file_names={"padding_oracle.zip"}>
                <p>Der Server wird dir beim Verbindungsaufbau eine Nachricht mit einer Flagge schicken. Du kannst mit dem Server über die bereitgestellte Library <i>Exploit.jar</i> und die dazugehörige <code>Connection</code>-Klasse kommunizieren. Die Nachricht wird im CBC-Modus verschlüsselt, allerdings kennst du den verwendeten Schlüssel nicht. Um beliebig lange Nachrichten schicken zu können, verwendet der Server das Padding-Schema <em>PKCS#7</em>.</p>
                <p>Nachdem dir der Server eine Nachricht geschickt hat, gibt er dir die Möglichkeit, ihm eine (hexadezimal kodierte) Nachricht mit IV zur Entschlüsselung zu schicken. Wenn die Entschlüsselung erfolgreich war, wird er mit der Nachricht "OK!" antworten, sonst mit einer entsprechenden Fehlermeldung.</p>
            </Task>
        );
    }
}
