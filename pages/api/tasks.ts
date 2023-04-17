import {NextApiRequest, NextApiResponse} from "next";
import {withIronSessionApiRoute} from "iron-session/next";
import {sessionOptions} from "../../lib/config";
import {getTasksForUser} from "../../lib/database";

export default withIronSessionApiRoute(tasksRoute, sessionOptions);

async function tasksRoute(req: NextApiRequest, res: NextApiResponse) {
	if (req.session["user"]) {
		const tasks = await getTasksForUser(req.session["user"].name);
		res.status(200).json({"success": true, "data": tasks});
	} else {
		res.status(200).json({"success": false, "error": "You are currently not logged in"});
	}
}
