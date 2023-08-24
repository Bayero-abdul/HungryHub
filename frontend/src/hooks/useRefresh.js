import axios from "../api/axios";
import { useAuth  } from "./useAuth";


const useRefreshToken = () => {
    const { setAuth } = useAuth();

    const refresh = async () => {
        try {
            const accessToken = sessionStorage.getItem("Token");
            console.log("from useRefresh", accessToken);
            
            const headers = {
                    'Content-Type': 'application/json;',
                    'Accept': 'application/json',
                    'Origin': 'http://localhost:5001', 
                    'Authorization': `Bearer ${accessToken}`    
            }
            const response = await fetch('http://127.0.0.1:5000/api/v1/refresh', {
                method: 'POST',
                headers: headers,
            });
            // const response = await fetch.post('/api/v1/refresh', axiosConfig);
            const data = await response.json();
            setAuth(prev => {

                console.log(JSON.stringify(prev));
                console.log(data.access_token);
                return { ...prev, access_token: data.access_token }
            });
            return data.access_token;
        } catch (err) {
            console.log("connection Error");
        } 
    }
    return refresh;
}

export default useRefreshToken;