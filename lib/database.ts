import {Database} from 'sqlite3';
import SHA256 from "crypto-js/sha256";
import HEX from "crypto-js/enc-hex";

const db = new Database('test.db');

export type User = {
    id: number,
    name: string
}

export type Task = {
    id: number,
    name: string,
    solved: boolean
}

export async function userExists(user: string): Promise<boolean> {
    return new Promise<boolean>((resolve, reject) => {
        db.prepare("SELECT * from users where name = ?")
        .get([user], (err: Error | null, row) => {
            if (err) { reject(err); return; }
            resolve(row !== undefined);
        });
    });
}

export async function loginAsUser(user: string, password: string): Promise<User> {
    return new Promise<User>((resolve, reject) => {
        db.prepare("SELECT * from users where name = ?")
            .get([user], (err: Error | null, row) => {
                if (err) { reject(err); return; }
                if (row === undefined) { resolve(undefined); return; }

                const hashedPassword = SHA256(password + row["salt"]).toString(HEX);
                const user = row["password"] === hashedPassword ? {id: row["id"], name: row["name"]} : undefined;
                resolve(user);
            });
    });
}

export async function getAllTasks(): Promise<Task[]> {
    return new Promise<Task[]>((resolve, reject) => {
        db.all("SELECT id, name from tasks", (err : Error | null, rows) => {
            if (err) { reject(err); return; }
            resolve(rows.map(r => ({id: r["id"], name: r["name"], solved: false})));
        });
    });
}

export async function getTasksForUser(user: string): Promise<Task[]> {
    return new Promise<Task[]>((resolve, reject) => {
        db.prepare("SELECT TaskID as 'id', Taskname as 'name', Solved from user_solved where username = ?")
            .all([user], (err: Error | null, rows: Task[]) => {
                if (err) { reject(err); return; }
                resolve(rows);
            });
    });
}