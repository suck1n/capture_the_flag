import React, {Component} from "react";
import Link from "next/link";
import styles from "./Mainwrapper.module.css";
import {LoginGetResponse} from "../pages/api/login";

type MainWrapperState = {
    response: LoginGetResponse,
    error: string,
    hideMenu: boolean
}

export default class MainWrapper extends Component<any, MainWrapperState> {

    constructor(props) {
        super(props);
        this.state = {response: undefined, error: "", hideMenu: true};
    }

    componentDidMount() {
        fetch("/api/login").then(d => d.json())
            .then((data: LoginGetResponse) => this.setState(prev => ({...prev, response: data})))
            .catch(err => this.setState(prev => ({ ...prev, error: err.toString()})));
    }

    handleMenuClick = () => {
        this.setState(prev => ({...prev, hideMenu: !prev.hideMenu}))
    }

    render() {
        if (this.state.error) {
            return <p>An error occurred: <br/> {this.state.error}</p>
        }

        if (!this.state.response) {
            return <p>Loading...</p>
        }

        if (!this.state.response.loggedIn) {
            return <p>Not logged in!</p>
        }

        return <>
            <div style={{color: "#3070b3", textAlign: "right", fontSize: "1.3rem"}}>signed in as {this.state.response.name}</div>
            <h1>Scoreboard Capture-The-Flag</h1>
            <div className={styles.navtoggle}>
                <button onClick={this.handleMenuClick}>Menu</button>
            </div>
            <nav className={styles.navbar} aria-hidden={this.state.hideMenu}>
                <div>
                    <Link href={"/scoreboard"}>Scoreboard</Link>
                    <Link href={"/tasks"}>Tasks</Link>
                    <Link href={"/logout"}>Logout</Link>
                </div>
            </nav>
            <main className={styles.main}>{this.props.children}</main>
        </>;
    }
}