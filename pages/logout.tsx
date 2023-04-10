import React, {Component} from "react";
import {NextRouter, withRouter} from "next/router";
import {LogoutResponse} from "./api/logout";


type LogoutState = {
    error?: string
}

type LogoutProps = {
    router: NextRouter
}


class Logout extends Component<LogoutProps, LogoutState> {

    constructor(props: LogoutProps) {
        super(props);

        this.state = { error: undefined }
    }

    componentDidMount() {
        fetch("/api/logout", { method: "POST" })
            .then(d => d.json())
            .then((d: LogoutResponse) => {
                if (d.success) {
                    void this.props.router.push("/");
                } else {
                    this.setState({ error: d.error})
                }
            })
            .catch(err => this.setState({ error: err.toString() }))
    }

    render() {
        if (this.state.error) {
            return <p>An error occurred while logging out: <br/>{this.state.error}</p>
        }

        return <p>Login out...</p>
    }
}

export default withRouter(Logout);