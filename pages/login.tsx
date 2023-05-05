import React, {Component} from "react";
import {NextRouter, withRouter} from "next/router";
import {LoginPostResponse} from "./api/login";
import styles from "../components/Login.module.css";
import Link from "next/link";
import Head from "next/head";

type LoginState = {
    username: string
    password: string
    error: string
}

type LoginProps = {
    router: NextRouter,
    query: any
}


class Login extends Component<LoginProps, LoginState> {

    constructor(props: LoginProps) {
        super(props);

        this.state = { username: this.props.router.query.username as string || "", password: "", error: "" };
    }

    static getInitialProps({query}) {
        return {query}
    }

    handleInputChange = (event: React.ChangeEvent<HTMLInputElement>) => {
        const { name, value } = event.target;
        this.setState((prev) => ({ ...prev, [name]: value }));
    }

    handleSubmit = async (event: React.FormEvent<HTMLFormElement>) => {
        event.preventDefault();

        try {
            const response = await fetch("/api/login", {
                method: "POST",
                headers: {"Content-Type": "application/json"},
                body: JSON.stringify({username: this.state.username, password: this.state.password}),
            });

            const data: LoginPostResponse = await response.json();

            if (data.success) {
                await this.props.router.push("/");
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
                    <title>Login</title>
                </Head>
                <div className={styles.container}>
                    <h1 className={styles.center}>Login</h1>
                    <form onSubmit={this.handleSubmit} className={styles.form}>
                        <div>
                            <label>Username:</label>
                            <input type="text" name="username" value={this.state.username} onChange={this.handleInputChange}/>
                        </div>
                        <div>
                            <label>Password:</label>
                            <input type="password" name="password" value={this.state.password} onChange={this.handleInputChange}/>
                        </div>
                        <div className={styles.buttons}>
                            <button onClick={() => console.log("TODO")}>Guest</button>
                            <button type="submit">Login</button>
                        </div>
                    </form>
                    <p className={styles.p}>Not yet registered? Create account <Link href={"/register"}>here</Link></p>
                    {this.state.error && <p style={{textAlign: "center"}}>{this.state.error}</p>}
                </div>
            </>
        );
    }
}

export default withRouter(Login);