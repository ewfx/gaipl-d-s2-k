import React, { useState } from "react";
import { AppBar, Toolbar, Typography, TextField, Button, Paper, Box, Container } from "@mui/material";

const App: React.FC = () => {
  const [messages, setMessages] = useState<{ text: string; sender: string }[]>([]);
  const [input, setInput] = useState("");

  const handleSendMessage = () => {
    if (!input.trim()) return;

    const newMessage = { text: input, sender: "user" };
    setMessages([...messages, newMessage]);
    setInput("");

    // Simulate chatbot response
    setTimeout(() => {
      setMessages((prevMessages) => [
        ...prevMessages,
        { text: `You said: ${input}`, sender: "bot" },
      ]);
    }, 1000);
  };

  return (
    <Box display="flex" flexDirection="column" height="100vh" bgcolor="#f4f6f8">
      {/* Header */}
      <AppBar position="static" color="primary">
        <Toolbar>
          <Typography variant="h6">Platform Buddy</Typography>
        </Toolbar>
      </AppBar>

      {/* Main Content */}
      <Box display="flex" flex={1}>
        <Box flex={1} p={5}>
          <TextField fullWidth variant="outlined" placeholder="Search..." sx={{ mt: 2 }} />
        </Box>

        {/* Chatbot Panel */}
        <Paper
          sx={{
            width: "30%",
            display: "flex",
            flexDirection: "column",
            p: 3,
            boxShadow: 3,
            borderRadius: 3,
            height: "80vh",
            m: 3,
          }}
        >
          <Typography variant="h5" fontWeight="bold" textAlign="center" gutterBottom>
            Chatbot
          </Typography>
          <Box flex={1} overflow="auto" p={2} bgcolor="#e3f2fd" borderRadius={2}>
            {messages.map((msg, index) => (
              <Box
                key={index}
                sx={{
                  mb: 1,
                  p: 1.5,
                  borderRadius: 2,
                  maxWidth: "75%",
                  alignSelf: msg.sender === "user" ? "flex-end" : "flex-start",
                  bgcolor: msg.sender === "user" ? "#1976d2" : "#eeeeee",
                  color: msg.sender === "user" ? "white" : "black",
                }}
              >
                {msg.text}
              </Box>
            ))}
          </Box>
          <Box display="flex" mt={2}>
            <TextField
              fullWidth
              variant="outlined"
              value={input}
              onChange={(e) => setInput(e.target.value)}
              placeholder="Type a message..."
            />
            <Button variant="contained" color="primary" sx={{ ml: 1 }} onClick={handleSendMessage}>
              Send
            </Button>
          </Box>
        </Paper>
      </Box>

      {/* Footer */}
      <Box component="footer" bgcolor="primary.main" color="white" py={2} textAlign="center">
        <Typography variant="body2">© 2025 Platform Buddy. All rights reserved.</Typography>
      </Box>
    </Box>
  );
};

export default App;
