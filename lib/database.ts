import {Database} from 'sqlite3';
import SHA256 from "crypto-js/sha256";
import HEX from "crypto-js/enc-hex";
import * as crypto from "crypto";

const db = new Database('capture_the_flag.db');

export type Flag = {
    id: number,
    flag: string,
    claimed: boolean,
    taskId: number
}

export type User = {
    id: number,
    name: string,
    tasks?: Task[]
}

export type Task = {
    id: number,
    name: string,
    position?: number,
    solved?: boolean
}

export type UserTask = {
    tasks: Task[],
    users: User[]
}

export async function getFlag(flag: string): Promise<Flag> {
    return new Promise<Flag>((resolve, reject) => {
        db.prepare("SELECT * from flags where flag = ?")
            .get([flag], (err: Error | null, row: Flag) => {
                if (err) { reject(err); return; }

                resolve(row);
            });
    });
}

export async function claimFlag(userId: number, flag: string): Promise<void> {
    return new Promise<void>((resolve, reject) => {
        db.prepare("INSERT INTO solved (userId, taskId) VALUES (?, (select taskId from flags where flag = ?))")
            .run([userId, flag], (err: Error | null) => {
                if (err) { reject(err); return; }
                db.prepare("UPDATE flags SET claimed = true WHERE flag = ?")
                    .run([flag], (err: Error | null) => {
                        if (err) { reject(err); return; }
                        resolve();
                    });
            });
    });
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

export async function createUser(user: string, password: string): Promise<void> {
    return new Promise<void>((resolve, reject) => {
        const salt = crypto.randomBytes(128).toString('hex');
        const hashedPassword = SHA256(password + salt).toString(HEX).toUpperCase();

        db.prepare("INSERT INTO users (name, password, salt) VALUES (?, ?, ?)")
            .run([user, hashedPassword, salt], (err: Error | null) => {
                if (err) { reject(err); return; }
                resolve();
            });
    });
}

export async function loginAsUser(user: string, password: string): Promise<User> {
    return new Promise<User>((resolve, reject) => {
        db.prepare("SELECT * from users where name = ?")
            .get([user], (err: Error | null, row) => {
                if (err) { reject(err); return; }
                if (!row) { resolve(undefined); return; }


                const hashedPassword = SHA256(password + row["salt"]).toString(HEX).toUpperCase();
                const user = row["password"] === hashedPassword ?
                    {id: row["id"], name: row["name"]} as User : undefined;
                resolve(user);
            });
    });
}

export async function getUsers(): Promise<User[]> {
    return new Promise<User[]>((resolve, reject) => {
        db.all("SELECT id, name from users", async (err : Error | null, rows: User[]) => {
            if (err) { reject(err); return; }

            for (let u of rows) {
                u.tasks = await getTasksForUser(u.id);
            }

            resolve(rows);
        });
    });
}


export async function getTasksForUser(user: number): Promise<Task[]> {
    return new Promise<Task[]>((resolve, reject) => {
        db.prepare("SELECT taskId as id, taskname as name, position, solved from user_tasks where UserID = ?")
            .all([user], (err: Error | null, rows: Task[]) => {
                if (err) { reject(err); return; }
                resolve(rows);
            });
    });
}

export async function getTasks(): Promise<Task[]> {
    return new Promise<Task[]>((resolve, reject) => {
        db.all("SELECT id, name from tasks", (err : Error | null, rows: Task[]) => {
            if (err) { reject(err); return; }
            resolve(rows);
        });
    });
}

export async function hasTaskCompleted(userId: number, taskId: number): Promise<Boolean> {
    return new Promise<Boolean>((resolve, reject) => {
        db.prepare("SELECT * from solved where userId = ? and taskId = ?")
            .get([userId, taskId], (err: Error | null, rows: any) => {
                if (err) { reject(err); return; }
                resolve(rows && rows.length == 1);
            });
    });
}

export async function getTasksAndUsers(): Promise<UserTask> {
    return ({tasks: await getTasks(), users: await getUsers()} as UserTask);
}