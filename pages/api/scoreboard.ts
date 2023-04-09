import {NextApiRequest, NextApiResponse} from "next";
import {withIronSessionApiRoute} from "iron-session/next";
import {sessionOptions} from "../../lib/config";
import {getTasksAndUsers, UserTask} from "../../lib/database";

export default withIronSessionApiRoute(scoreboardRoute, sessionOptions);

export type ScoreboardResponse = {
    userTasks?: UserTask,
    error?: string
}

async function scoreboardRoute(req: NextApiRequest, res: NextApiResponse) {
    const user = req.session["user"];

    if (!user) {
        res.status(401).json({ error: "Not logged in" });
        return;
    }

    const usersWithTasks: UserTask = await getTasksAndUsers();

    if (usersWithTasks) {
        res.status(200).json({ userTasks: usersWithTasks } as ScoreboardResponse);
    } else {
        res.status(404).json({ error: "No users/tasks exist" } as ScoreboardResponse);
    }
}