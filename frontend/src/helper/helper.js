
const verifyToken = () => {
    if (localStorage.getItem("token")) {
        return true
    }
    return false
}

export { verifyToken }