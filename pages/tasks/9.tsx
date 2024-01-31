import React, {Component} from "react";
import Task from "../../components/Task";

export default class LotteryV2 extends Component<any, any> {

    constructor(props) {
        super(props);
    }

    render() {

        return (
            <Task title={"Fallmerayer Lottery v2"} id={9} file_names={"lottery_v2.zip"}>
                <p>Eine weitere Version von <em>Fallmerayer Lottery</em>, die ebenfalls ein Problem mit ihrer Nutzung von Zufallszahlengeneratoren hat. Diese Version nutzt für die Erzeugung der Zufallszahlen den Generator <a href="https://en.wikipedia.org/wiki/Xorshift" >XORShift32</a>. Eine Variante dieses Generators <strong>XORShift128+</strong> wird in der Javascript Engine von Google Chrome eingesetzt für die Implementierung von <code>math.rand()</code>.</p>
                <p>Spiel das Spiel und gewinne! Kannst du die Zufallszahlen des kommenden Tages voraussagen?</p>
            </Task>
        );
    }
}
