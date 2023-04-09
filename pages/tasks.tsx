import React, {Component} from "react";
import {NextRouter, withRouter} from "next/router";
import MainWrapper from "../components/MainWrapper";
import styles from "../components/Tasks.module.css";
import {FontAwesomeIcon} from "@fortawesome/react-fontawesome";
import {faCheck} from "@fortawesome/free-solid-svg-icons";
import {UserResponse} from "./api/user";
import Link from "next/link";

type TasksProps = {
    router: NextRouter;
}

class Tasks extends Component<TasksProps, UserResponse> {

    constructor(props) {
        super(props);
        this.state = { user: undefined, tasks: undefined, error: "" };
    }

    async componentDidMount() {
        fetch("/api/user").then(d => d.json())
            .then((data: UserResponse) => this.setState(data))
            .catch(err => this.setState({ error: err }));
    }

    render() {
        if (this.state.error) {
            return <p>An error occurred: <br/> {this.state.error}</p>
        }

        if (!this.state.user) {
            return <p>Loading...</p>;
        }

        return (
            <MainWrapper>
                <table className={styles.table}>
                    <thead>
                        <tr>
                            <th>#</th>
                            <th>Name</th>
                            <th>Solved</th>
                        </tr>
                    </thead>
                    <tbody>
                        {this.state.tasks.map(t => <tr key={t.id}>
                            <td>{t.id}</td>
                            <td><Link href={"/tasks/" + t.id}>{t.name}</Link></td>
                            <td>{t.solved ? <FontAwesomeIcon icon={faCheck}/> : <></>}</td>
                        </tr>)}
                    </tbody>
                </table>
            </MainWrapper>
        );
    }
}

export default withRouter(Tasks);
