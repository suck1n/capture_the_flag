import React, {Component} from "react";
import Task from "../../components/Task";

export default class XSS extends Component<any, any> {

    constructor(props) {
        super(props);
    }

    render() {

        return (
            <Task title={"XSS (Cross-Site-Scripting)"} id={6} file_names={"xss.zip"} httpOnly={true}>
                <p>Die Bank der Fallmerayer hat eine Testversion ihrer Webseite herausgebracht.</p>
                <p>Der Admin der Webseite ist über ein Kontaktformular erreichbar und wird liebend gerne auf jeden Phishing-Link klicken, den du ihm über dieses Formular zukommen lasst. Er nutzt als Browser eine aktuelle Version von Chromium. Führe auf diese Weise einen XSS-Angriff auf die Webseite durch! (<strong>Achtung:</strong> Bitte schicke <strong>nur</strong> den Link ohne a-Tag oder Phishing Text).</p>
                <p>Die Flagge ist auf der Seite mit den Umsätzen des Admins versteckt.</p>
            </Task>
        );
    }
}
