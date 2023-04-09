import {NextApiRequest, NextApiResponse} from "next";
import {withIronSessionApiRoute} from "iron-session/next";
import {sessionOptions} from "../../lib/config";
import {getTasksForUser, Task, User} from "../../lib/database";

export default withIronSessionApiRoute(userRoute, sessionOptions);

export type UserResponse = {
	user: User,
	tasks: Task[]
	error?: string
}

async function userRoute(req: NextApiRequest, res: NextApiResponse) {
	const user = req.session["user"];

	if (!user) {
		res.status(401).json({ error: "Not logged in" });
		return;
	}

	const userTasks: Task[] = await getTasksForUser(user.id);

	if (userTasks) {
		res.status(200).json({
			user: user,
			tasks: userTasks,
		} as UserResponse);
	} else {
		res.status(404).json({ error: "User has no tasks" } as UserResponse);
	}
}