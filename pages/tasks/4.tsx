import React, {Component} from "react";
import Task from "../../components/Task";

export default class ManInTheMiddleAttack extends Component<any, any> {

    constructor(props) {
        super(props);
    }

    render() {

        return (
            <Task title={"Man-In-The-Middle-Attack"} id={4} path={":1024"} file_names={["mitma.zip", "template.py"]}>
                <p>Das Server Skript stellt eine Verbindung zwischen zwei Parteien her, und leitet deren Nachrichten unverändert weiter. Zur sicheren Kommunikation vereinbaren beide Parteien zunächst mit Hilfe des Diffie-Hellman-Verfahrens einen gemeinsamen Schlüssel k.</p>
                <p>Im Anschluss schickt Partei A mit AES-CBC verschlüsselte Nachrichten an Partei B. Der verwendete Schlüssel besteht dabei aus den ersten 16 Bytes des SHA-512-Hashes von k. Für bessere Sicherheit verwenden die beiden Parteien HMAC-SHA256 als Integritätsschutz (allerdings im MAC-then-Encrypt-Modus) sowie einen zufälligen IV, der jeweils der Nachricht vorangestellt wird.</p>
                <p><strong>Hinweis:</strong> Nutze für die Operation k entweder die Python-Funktion <code>pow(a, b, p)</code> oder die Java-Funktion <code>new BigInteger(a).modPow(b, p)</code>.</p>
		<p><strong>Hinweis:</strong> Sieh dir dieses Video für eine Erklärung des DH-Algorithmuses an: <a href={"https://www.youtube.com/watch?v=3QnD2c4Xovk"}>https://www.youtube.com/watch?v=3QnD2c4Xovk</a></p>
            </Task>
        );
    }
}
