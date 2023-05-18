import React, {Component} from "react";
import Task from "../../components/Task";

export default class SQLInjection extends Component<any, any> {

    constructor(props) {
        super(props);
    }

    render() {

        return (
            <Task title={"SQL-Injection"} id={1} file_names={"suchmaschine.zip"}>
                <p>Die Schule hat eine kleine Suchmaschine zusammengestellt, diese hat jedoch eine SQL-Injection-Vulnerability.<br/>Die Suchmaschine dient hauptsächlich zum Durchsuchen des Intranets (Webseiten von Schülern, etc.), es hat aber auch "versteckte" Seiten indiziert und in ihrer SQLite-Datenbank gespeichert. Einer dieser Einträge enthält die Flagge. Erstelle eine präparierte Suchanfrage mit SQL-Injection, die die Flagge aus der SQLite-Datenbank extrahiert.<br/>Die Datenbanktabelle intranet_index ist wie folgt aufgebaut:</p>
                <table>
                    <thead>
                    <tr>
                        <th><code>id</code></th>
                        <th><code>title</code></th>
                        <th><code>url</code></th>
                        <th><code>is_secret</code></th>
                    </tr>
                    </thead>
                    <tbody>
                    <tr>
                        <td>1</td>
                        <td>Very Cool Site</td>
                        <td>https://www.fallmerayer.it</td>
                        <td>0</td>
                    </tr>
                    <tr>
                        <td>2</td>
                        <td><code>flag&#123;...&#125;</code></td>
                        <td>...</td>
                        <td>1</td>
                    </tr>
                    <tr>
                        <td>...</td>
                        <td>...</td>
                        <td>...</td>
                        <td>...</td>
                    </tr>
                    </tbody>
                </table>
                <p>Die Suchmaschine benutzt folgende SQL-Anfrage für die Suche nach einer Webseite:</p>
                <div className="codehilite">
                <pre>
                    <code>
                        <span className="k">SELECT </span>
                        <span className="o">* </span>
                        <span className="k">FROM </span>
                        <span className="n">intranet_index </span>
                        <span className="k">WHERE </span>
                        <span className="n">is_secret </span>
                        <span className="o">= </span>
                        <span className="mi">0 </span>
                        <span className="k">AND </span>
                        <span className="n">title </span>
                        <span className="k">LIKE </span>
                        <span className="s1">'%&lt;your_search_term&gt;%'</span>
                    </code>
                </pre>
                </div>
                <p>Den vollständigen Quelltext des Servers findest du weiter unten.</p>
                <p><strong>Hinweis:</strong> Eine Übersicht der gängigsten SQL-Statements kannst du z.B. <a href="http://www.sqltutorial.org/wp-content/uploads/2016/04/SQL-cheat-sheet.pdf">hier</a> finden.</p>
                <p><strong>Hinweis:</strong> SQL-Statements können mit einem Strichpunkt ';' beendet werden</p>
                <p><strong>Hinweis:</strong> SQL-Statements können mit zwei Minuse '--' auskommentiert werden</p>
            </Task>
        );
    }
}
