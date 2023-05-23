import React, {Component} from "react";
import Task from "../../components/Task";

export default class CSRF extends Component<any, any> {

    constructor(props) {
        super(props);
    }

    render() {

        return (
            <Task title={"Cross Site Request Forgery"} id={5} file_names={"csrf.zip"}>
                <p>Die Informatiklehrer werden ab sofort eine neue Webseite verwenden, um den Schüler*innen die Zeugnisnote mitzuteilen. Leider steht schon fest, dass du wohl nicht bestehen wirst - dein Informatiklehrer hat dir bereits eine 4.0 eingetragen! Allerdings nimmt er noch Beschwerden entgegen, er könnte sich in deinem Fall also noch einmal umentscheiden... Wenn du es schaffst, deine Note auf 10.0 zu ändern, erhältst du als Belohnung eine Flagge!</p>
                <p><strong>Hinweis 1:</strong> Der Informatiklehrer nutzt eine aktuelle Version von Chromium. Er weiß genug von IT-Sicherheit, dass er nicht auf deine Links klicken wird.</p>
                <p><strong>Hinweis 2:</strong> Beim Bearbeiten deiner Beschwerde, schaut sich der Lehrer auch dein Profil an!</p>
            </Task>
        );
    }
}