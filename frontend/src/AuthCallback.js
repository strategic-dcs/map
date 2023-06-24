import React, { useEffect, useState } from 'react';
import { Navigate, useLocation } from "react-router-dom";
import axios from 'axios';
import Cookies from 'js-cookie';

const AuthCallback = () => {
  const location = useLocation();

  console.log('[callback] HERE location: ', location)
  const [isLoggedIn, setIsLoggedIn] = useState(false);

  useEffect(() => {
    const searchParams = new URLSearchParams(location.search);
    const code = searchParams.get('code');

    console.log("[callback] HERE code: " + code);

    if (code && isLoggedIn === false) {
      // ideally this should be hitting the same domain/port and bring proxied to the backend =/
      // but I couldn't get the proxy to work.
      axios.get(`http://localhost:8000/api/auth/callback?code=${code}`)
        .then(response => {
          console.log(response.data);
          const accessToken = response.data.access_token;
          Cookies.set('access_token', accessToken);

          setIsLoggedIn(true);
        })
        .catch(error => {
          console.log(error);
        });
    }
  }, []);


  if (!isLoggedIn)
    return <div>logging in...</div>
  else
    return <Navigate to="/" />;
};

export default AuthCallback;
