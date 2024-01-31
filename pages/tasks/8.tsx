import React, {Component} from "react";
import Task from "../../components/Task";

export default class CMDInjection extends Component<any, any> {

    constructor(props) {
        super(props);
    }

    render() {

        return (
            <Task title={"Command Injection"} id={8} file_names={"command.zip"}>
                <p>Viele Router bieten in ihrem Webinterface eine Diagnosemöglichkeit mittels <code>ping</code> an, um zu überprüfen ob andere Geräte im Netzwerk erreicht werden können. Auf vielen von ihnen, war dieses Feature in Vergangenheit schlecht implementiert, sodass es möglich war beliebige auf dem Router installierte Programme auszuführen. Die Informatiklehrer der Fallmerayer haben aber von diesem Angriff gelernt. Deshalb haben sie einige Gegenmaßnahmen bei ihrem neuen <em>Fallmerayer Router</em> getroffen. Kannst du trotzdem einen Fehler finden und das Programm <code>./flag</code> ausführen?</p>
                <p><strong>Hinweis:</strong> Du kannst dieses Problem ohne weiteres Vorwissen unter zu Hilfenahme der Manpage von <code>sh</code> lösen! (Also <code>man sh</code> entweder in Google oder in einer Konsole eingeben) </p>
            </Task>
        );
    }
}
