import React, {Component, PropsWithChildren} from "react";
import styles from "./Task.module.css";
import MainWrapper from "./MainWrapper";
import {NextRouter, withRouter} from "next/router";

type TaskProps = {
    title: string
    id: number
    path?: string
    file_names?: string[] | string | undefined
    router: NextRouter
}

class Task extends Component<PropsWithChildren<TaskProps>, any> {

    private readonly host : string;
    private readonly baseUrl: string;
    private readonly url: string;

    constructor(props: PropsWithChildren<TaskProps>) {
        super(props);

        this.host = typeof window !== "undefined" && window.location.host.replace(/:\d+/, "") || "";
        this.baseUrl = typeof window !== "undefined" && (window.location.protocol + "//" + this.host) || "";
        this.url = this.props.path ? this.host + this.props.path : this.baseUrl + ":" + (5000 + this.props.id);
    }

    getDownloadUrl(file: string) {
        return this.baseUrl + "/api/download?file=" + file;
    }

    render() {
        return <MainWrapper>
            <h2>Task {this.props.id}: {this.props.title}</h2>
            {this.props.children}
            <div>
                <b>URL: </b><a className={styles.a} href={this.props.path ? "" : this.url}>{this.url}</a>
                {typeof this.props.file_names !== "undefined" && <h3>Downloads</h3>}
                {typeof this.props.file_names !== "undefined" && (((typeof this.props.file_names !== "object" ? [this.props.file_names] : this.props.file_names) as string[])
                    .map(file => <><a key={file} className={styles.a} href={this.getDownloadUrl(file)}>{file}</a><br/></>))}
            </div>
        </MainWrapper>;
    }
}

export default withRouter(Task);
