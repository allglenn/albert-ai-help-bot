import React from 'react';
import { Box } from '@mui/material';
import Navbar from './Navbar';

const PrivateLayout = ({ children }) => {
    return (
        <Box sx={{ minHeight: '100vh', display: 'flex', flexDirection: 'column' }}>
            <Navbar />
            <Box sx={{ flex: 1, p: 3 }}>
                {children}
            </Box>
        </Box>
    );
};

export default PrivateLayout; 