import React, {Component} from "react";
import {NextRouter, withRouter} from "next/router";
import {LoginPostResponse} from "./api/login";

type LoginState = {
    username: string
    password: string
    error: string
}

type LoginProps = {
    router: NextRouter
}


class Login extends Component<LoginProps, LoginState> {

    constructor(props: LoginProps) {
        super(props);

        this.state = { username: "", password: "", error: "" };
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
            <div>
                <h1>Login</h1>
                <form onSubmit={this.handleSubmit}>
                    <label>
                        Username:
                        <input
                            type="text"
                            name="username"
                            value={this.state.username}
                            onChange={this.handleInputChange}
                        />
                    </label>
                    <br />
                    <label>
                        Password:
                        <input
                            type="password"
                            name="password"
                            value={this.state.password}
                            onChange={this.handleInputChange}
                        />
                    </label>
                    <br />
                    <button type="submit">Login</button>
                    {this.state.error && <p>{this.state.error}</p>}
                </form>
            </div>
        );
    }
}

export default withRouter(Login);