import React, {Component} from "react";
import Task from "../../components/Task";

export default class BlindSQLInjection extends Component<any, any> {

    constructor(props) {
        super(props);
    }

    render() {

        return (
            <Task title={"Blind-SQL-Injection"} id={2} file_names={"socialnetwork.zip"}>
                <p>Versuche dich im Folgenden an einer Blind-SQL-Injection im Anmeldedialog des fiktiven sozialen Netzwerkes <em>Fallmerayer+</em>. Bei erfolgreicher Anmeldung des Users <code>admin</code> erhält dieser eine Flagge. Sowohl das Nutzernamen- als auch das Passwort-Feld sind über eine SQL-Injection angreifbar.</p>
                <p>Unten findest du zum Download den Server-Code für diese Aufgabe.</p>
                <p><strong>Hinweis:</strong> Es empfiehlt sich einen Exploit für diese Aufgabe zu schreiben (z.B. in Python)!</p>
            </Task>
        );
    }
}
