import {NextApiRequest, NextApiResponse} from "next";


export default function userRoute(req: NextApiRequest, res: NextApiResponse) {

	res.status(200).send({"status": "todo"});
}