export const getClassOverview = () => http.get("/class-view/overview"); 
export const getClassDetails = (classId) => http.get(/class-view/details?class=${classId});