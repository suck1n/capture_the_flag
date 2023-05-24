import React, {Component, PropsWithChildren} from "react";
import styles from "./Task.module.css";
import MainWrapper from "./MainWrapper";
import {NextRouter, withRouter} from "next/router";

type TaskProps = {
    title: string
    id: number
    httpOnly?: boolean
    path?: string
    file_names?: string[] | string | undefined
    router: NextRouter
}

class Task extends Component<PropsWithChildren<TaskProps>, any> {

    private readonly host : string;
    private readonly protocol : string;
    private readonly baseUrl: string;
    private readonly url: string;

    constructor(props: PropsWithChildren<TaskProps>) {
        super(props);
	
	
        this.host = typeof window !== "undefined" && window.location.host.replace(/:\d+/, "") || "";
	this.protocol = typeof window !== "undefined" && !this.props.httpOnly && window.location.protocol || "http:";
        this.baseUrl = typeof window !== "undefined" && (this.protocol + "//" + this.host) || "";
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
                {this.props.path ? <><b>IP: </b><span className={styles.a}>{this.url}</span></> : <><b>URL: </b><a className={styles.a} href={this.url}>{this.url}</a></>}
                <h3>Downloads</h3>
                <a className={styles.a} href={this.getDownloadUrl("Exploit.jar")}>Exploit.jar</a><br/>
                {typeof this.props.file_names !== "undefined" && (((typeof this.props.file_names !== "object" ? [this.props.file_names] : this.props.file_names) as string[])
                    .map(file => <><a key={file} className={styles.a} href={this.getDownloadUrl(file)}>{file}</a><br/></>))}
            </div>
        </MainWrapper>;
    }
}

export default withRouter(Task);
