import { Button, Dialog, DialogActions, DialogContent, DialogContentText, DialogTitle, Modal } from '@mui/material';
import axios from 'axios';
import React, { createContext, useState, useRef } from 'react';


export const AxiosContext = createContext(null);

export const AxiosInstanceProvider = ({
    children,
}) => {

    const [errorContext, setErrorContext] = useState({
        'show': false,
        'body': 'This has all gone wrong',
        'title': 'Some Title',
    });

    const instanceRef = useRef(axios.create({}));

    instanceRef.current.interceptors.response.use((response) => response, (error) => {
        // We capture all 422 errors as these are generic information
        if (error?.response?.status === 422) {

            let issues = [];

            for (const item of error.response.data.detail) {
                issues.push(<li>{item.msg}: {item.loc[item.loc.length-1]}</li>)
            }

            setErrorContext({
                'title': 'Validation Error',
                'body': <>
                    There were errors encountered in the following items:
                    <ul>
                        {issues}
                    </ul>
                </>,
                'show': true,
            })
        } else if (error?.response?.status === 409) {
            // 409 is our general error, database, or such
            setErrorContext({
                'title': 'Request Error',
                'body': error.response.data.detail,
                'show': true,
            })
        } else if (error.code === 'ERR_NETWORK' || [504, 502].includes(error?.response?.status)) {
            // General API Access issues, 504 timeout, 502 bad gateway
            setErrorContext({
                'title': `Network Error`,
                'body': 'Unable to communicate with the API',
                'show': true,
            });
        } else if (error?.response) {
            // All other requests are uncaught expceptions
            setErrorContext({
                'title': `Uncaught Exception: ${error?.response?.status}`,
                'body': JSON.stringify(error.response.data),
                'show': true,
            })
        } else {
            setErrorContext({
                'title': `Uncaught Exception`,
                'body': error.message,
                'show': true,
            })
        }

        return Promise.resolve(null);

        // Consume the error and return null
        //return null
    });

    function handleClose() {
        setErrorContext({...errorContext, show: false});
    }

    return (
        <AxiosContext.Provider value={instanceRef.current}>
            {children}
            <Dialog open={errorContext.show}>
                <DialogTitle>{errorContext.title}</DialogTitle>
                <DialogContent>
                    <DialogContentText>{errorContext.body}</DialogContentText>
                </DialogContent>
                <DialogActions>
                    <Button autoFocus onClick={handleClose}>
                        Close
                    </Button>
                </DialogActions>
            </Dialog>
        </AxiosContext.Provider>
    );

};
