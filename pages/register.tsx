import React, {Component} from "react";
import {NextRouter, withRouter} from "next/router";
import styles from "../components/Login.module.css";
import Link from "next/link";
import {RegisterResponse} from "./api/register";
import Head from "next/head";
import {LoginGetResponse} from "./api/login";

type RegisterState = {
    username: string
    password: string
    error: string
    created: boolean
}

type RegisterProps = {
    router: NextRouter
}


class Register extends Component<RegisterProps, RegisterState> {

    constructor(props: RegisterProps) {
        super(props);

        this.state = { username: "", password: "", error: "", created: false };
    }

    componentDidMount() {
        fetch("/api/login").then(d => d.json())
            .then((data: LoginGetResponse) => {
                if (data.loggedIn) {
                    void this.props.router.push("/scoreboard");
                }
            })
            .catch(err => this.setState({ error: err.toString() }));
    }

    handleInputChange = (event: React.ChangeEvent<HTMLInputElement>) => {
        const { name, value } = event.target;
        this.setState((prev) => ({ ...prev, [name]: value }));
    }

    handleSubmit = async (event: React.FormEvent<HTMLFormElement>) => {
        event.preventDefault();

        try {
            const response = await fetch("/api/register", {
                method: "POST",
                headers: {"Content-Type": "application/json"},
                body: JSON.stringify({username: this.state.username, password: this.state.password}),
            });

            const data: RegisterResponse = await response.json();

            if (data.success) {
                this.setState({created: true});
            } else {
                this.setState(prev =>  ({...prev, error: data.error}));
            }
        } catch (error) {
            console.error(error);
            this.setState(prev =>  ({...prev, error: "An error occurred while logging in"}));
        }
    }

    render() {
        return (
            <>
                <Head>
                    <title>Register</title>
                </Head>
                <div className={styles.container}>
                    <h1 className={styles.center}>Register</h1>
                    <form onSubmit={this.handleSubmit} className={styles.form}>
                        <div>
                            <label>Username:</label>
                            <input type="text" name="username" value={this.state.username} onChange={this.handleInputChange}/>
                        </div>
                        <div>
                            <label>Password:</label>
                            <input type="password" name="password" value={this.state.password} onChange={this.handleInputChange}/>
                        </div>
                        <button type="submit">Register</button>
                    </form>
                    <p className={styles.p}>Already have an Account? Login <Link href={"/login"}>here</Link></p>
                    {this.state.error && <p style={{textAlign: "center"}}>{this.state.error}</p>}
                    {this.state.created && <p style={{textAlign: "center"}}>User created! You can now <Link href={"/login?username=" + this.state.username}>Login</Link></p>}
                </div>
            </>
        );
    }
}

export default withRouter(Register);