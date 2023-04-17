import React, {Component, PropsWithChildren} from "react";
import styles from "./Task.module.css";
import MainWrapper from "./MainWrapper";

type TaskProps = {
    title: string
    id: number
    download: Download
    url?: string
}

type Download = {
    url: string
    name: string
}

export default class Task extends Component<PropsWithChildren<TaskProps>, any> {

    render() {
        return <MainWrapper>
            <h2>Task {this.props.id}: {this.props.title}</h2>
            {this.props.children}
            <div>
                {this.props.url && <><b>URL: </b><a className={styles.a} href={this.props.url}>{this.props.url}</a></>}
                <h3>Downloads</h3>
                <a className={styles.a} href={this.props.download.url}>{this.props.download.name}</a>
            </div>
        </MainWrapper>;
    }
}
