import React, {Component} from "react";
import {NextRouter, withRouter} from "next/router";
import MainWrapper from "../components/MainWrapper";
import styles from "../components/Scoreboard.module.css";
import {ScoreboardResponse} from "./api/scoreboard";
import {FontAwesomeIcon} from "@fortawesome/react-fontawesome";
import {faCheck} from "@fortawesome/free-solid-svg-icons";

type ScoreboardProps = {
    router: NextRouter;
}

class Scoreboard extends Component<ScoreboardProps, ScoreboardResponse> {

    constructor(props) {
        super(props);
        this.state = { userTasks: undefined };
    }

    componentDidMount() {
        fetch("/api/scoreboard").then(d => d.json())
            .then((data: ScoreboardResponse) => {
                if (!data.error) {
                    data.userTasks.users = data.userTasks.users
                        .sort((u1, u2) => {
                            const u1TasksSolved = u1.tasks.filter(t => t.solved).length;
                            const u2TasksSolved = u2.tasks.filter(t => t.solved).length;

                            if (u1TasksSolved > u2TasksSolved) {
                                return -1;
                            } else if (u1TasksSolved < u2TasksSolved) {
                                return 1;
                            }

                            const u1Positions = u1.tasks.filter(t => t.solved).map(t => t.position).reduce((s, n) => s + n);
                            const u2Positions = u2.tasks.filter(t => t.solved).map(t => t.position).reduce((s, n) => s + n);

                            return u1Positions - u2Positions;
                        })
                }

                this.setState(data);
            })
            .catch(err => this.setState({ error: err }));
    }

    handleSubmit = (event: React.FormEvent<HTMLFormElement>) => {
        event.preventDefault();

        fetch("/api/flag", {
            method: "POST",
            headers: {"Content-Type": "application/json"},
            body: JSON.stringify({flag: event.currentTarget.getElementsByTagName("input")[0].value}),
        }).then(d => console.log("TODO: ", d));
    }

    render() {
        if (this.state.error) {
            return <p>An error occurred: <br/> {this.state.error}</p>
        }

        if (!this.state.userTasks) {
            return <p>Loading...</p>;
        }

        return (
            <MainWrapper>
                <form onSubmit={this.handleSubmit} className={styles.form}>
                    <input type={"text"} placeholder={"flag{...}"} name={"flag"}/>
                    <input type={"submit"} value={"Submit Flag"} className={"todo"}/>
                </form>
                <h2>Scoreboard</h2>
                <div className={styles.scoreboard}>
                    <table>
                        <thead>
                        <tr>
                            <th>#</th>
                            <th style={{paddingRight: "250px"}}>User</th>
                            {this.state.userTasks.tasks.map(task => <th key={task.id} title={task.name}>#{task.id}</th>)}
                        </tr>
                        </thead>
                        <tbody>
                        {this.state.userTasks.users.map((user, index) =>
                            <tr key={user.id}>
                                <td>{index + 1}</td>
                                <td>{user.name}</td>
                                {user.tasks.map((task) => (
                                        <td key={"task" + user.id + task.id} title={task.position + ". Abgabe"}>
                                            {task.solved ?
                                                <FontAwesomeIcon icon={faCheck} style={
                                                    task.position != 1 ? {fontSize: "1.3em"} : {fontSize: "1.3em", color: "red"}
                                                }/> : <></>}
                                        </td>
                                    ))
                                }
                            </tr>
                        )}
                        </tbody>
                    </table>
                </div>
            </MainWrapper>
        );
    }
}

export default withRouter(Scoreboard);
