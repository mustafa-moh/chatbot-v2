import React, { useState, useRef, useEffect } from 'react';
import { Box, TextField, Button, List, ListItem, ListItemText, Paper, Typography, CircularProgress } from '@mui/material';
import SendIcon from '@mui/icons-material/Send';

const ChatBot = () => {
    const [messages, setMessages] = useState([]);
    const [input, setInput] = useState('');
    const [sessionId, setSessionId] = useState('');
    const [isLoading, setIsLoading] = useState(false);
    const messagesEndRef = useRef(null);

    // Auto-scroll to the bottom of the chat
    const scrollToBottom = () => {
        messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
    };

    useEffect(() => {
        scrollToBottom();
    }, [messages]);

    const handleSend = async () => {
        if (!input.trim()) return;

        // Add user message to the chat
        setMessages((prev) => [...prev, { sender: 'user', text: input }]);
        setInput('');
        setIsLoading(true);

        // Call the API
        try {
            const response = await fetch(process.env.REACT_APP_API_URL, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ prompt: input, session_id: sessionId }),
            });

            const data = await response.json();

            // Update session ID if received
            if (data.session_id) {
                setSessionId(data.session_id);
            }

            // Add bot response to the chat
            setMessages((prev) => [...prev, { sender: 'bot', text: data.response }]);
        } catch (error) {
            console.error('Error calling API:', error);
            setMessages((prev) => [...prev, { sender: 'bot', text: 'Sorry, something went wrong!' }]);
        } finally {
            setIsLoading(false);
        }
    };

    return (
        <Box sx={{ height: '80vh', display: 'flex', flexDirection: 'column', justifyContent: 'space-between' }}>
            <Paper elevation={3} sx={{ flexGrow: 1, overflowY: 'auto', p: 2, mb: 2 }}>
                <List>
                    {messages.map((msg, index) => (
                        <ListItem key={index} sx={{ justifyContent: msg.sender === 'user' ? 'flex-end' : 'flex-start' }}>
                            <ListItemText
                                primary={msg.text}
                                secondary={msg.sender === 'user' ? 'You' : 'Bot'}
                                sx={{
                                    textAlign: msg.sender === 'user' ? 'right' : 'left',
                                    bgcolor: msg.sender === 'user' ? '#e3f2fd' : '#f5f5f5',
                                    p: 1,
                                    borderRadius: 2,
                                    maxWidth: '70%',
                                }}
                            />
                        </ListItem>
                    ))}
                    {isLoading && (
                        <ListItem sx={{ justifyContent: 'flex-start' }}>
                            <ListItemText
                                primary={<Typography sx={{ color: '#666' }}>Bot is typing...</Typography>}
                                sx={{
                                    bgcolor: '#f5f5f5',
                                    p: 1,
                                    borderRadius: 2,
                                    maxWidth: '70%',
                                }}
                            />
                        </ListItem>
                    )}
                    <div ref={messagesEndRef} />
                </List>
            </Paper>
            <Box sx={{ display: 'flex', gap: 1 }}>
                <TextField
                    fullWidth
                    variant="outlined"
                    placeholder="Type a message..."
                    value={input}
                    onChange={(e) => setInput(e.target.value)}
                    onKeyPress={(e) => e.key === 'Enter' && handleSend()}
                />
                <Button variant="contained" color="primary" onClick={handleSend} disabled={isLoading} endIcon={<SendIcon />}>
                    {isLoading ? <CircularProgress size={24} /> : 'Send'}
                </Button>
            </Box>
        </Box>
    );
};

export default ChatBot;