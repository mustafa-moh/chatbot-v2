import React from 'react';
import ChatBot from './ChhatBot';
import { Container, Typography, CssBaseline, Box } from '@mui/material';
// import logo from './logo.png'; // Add your logo image to the src folder

function App() {
    return (
        <Container maxWidth="sm" sx={{ mt: 4 }}>
            <CssBaseline />
            <Box sx={{ display: 'flex', justifyContent: 'center', mb: 3 }}>
                {/*<img src={logo} alt="Chat Bot Logo" style={{ width: '100px', height: '100px' }} />*/}
            </Box>
            <Typography variant="h4" align="center" gutterBottom>
                Chat Bot Application
            </Typography>
            <ChatBot />
        </Container>
    );
}

export default App;