import React, {Component} from "react";
import Task from "../../components/Task";

export default class SQLUnion extends Component<any, any> {

    constructor(props) {
        super(props);
    }

    render() {

        return (
            <Task title={"SQL Union Injection"} id={7} file_names={"union.zip"}>
                <p>Wir haben unsere unsichere Suchmaschine um das Premiumfeature Fallmerayer+ erweitert. Leider ist der Login-Dialog noch nicht vorhanden. Allerdings existiert bereits die Datenbanktabelle <code>falloogleplus_users</code>. Diese Tabelle ist wie folgt aufgebaut:</p>
                <table>
                   <thead>
                       <tr>
                           <th><code>id</code></th>
                           <th><code>username</code></th>
                           <th><code>password</code></th>
                       </tr>
                   </thead>
                   <tbody>
                        <tr>
                            <td>1</td>
                            <td><code>admin</code></td>
                            <td><code>flag&#123;...&#125;</code></td>
                        </tr>
                        <tr>
                            <td>...</td>
                            <td>...</td>
                            <td>...</td>
                        </tr>
                    </tbody>
                </table>
                <p>Die Flagge befindet sich in der Passwort-Spalte für den User <code>admin</code>. Das SQL-Query für die eigentliche Suche nach Seiten hat sich nicht verändert. Extrahiere die Flagge! Den vollständigen Server-Quelltext findest du wie üblich im Anhang zu dieser Aufgabe.</p>
            </Task>
        );
    }
}
