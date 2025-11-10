export const classOverview = [ 
	{ classId: "dbo:StadiumShape", violationsCount: 2379 }, 
	{ classId: "dbo:AmphibianShape", violationsCount: 729 }, 
	{ classId: "dbo:ComicStripShape", violationsCount: 718 }, 
	{ classId: "dbo:CongressmanShape", violationsCount: 1896 }, ]; 
export const classDetails = (classId) => (
	{ classId, examples: [ 
	{ node: "dbr:Item1", path: "rdf:type", message: "min count contraint component" }, 
	{ node: "dbr:Item1", path: "rdf:type", message: "in constraint component" }, 
	{ node: "dbr:Item1", path: "rdf:type", message: "class constraint component" }, ], });