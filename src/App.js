import {
  Box,
  Button,
  Container,
  CssBaseline,
  List,
  ListItem,
  ListItemText,
  Paper,
  TextField,
  Typography
} from '@mui/material';
import axios from 'axios';
import React, { useEffect, useState } from 'react';
import OEEDashboard from './components/OEEDashboard';

function App() {
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState('');
  const [loading, setLoading] = useState(false);
  const [filters, setFilters] = useState({
    device_id: '',
    location: '',
    month: ''
  });
  const [availableFilters, setAvailableFilters] = useState({
    device_ids: [],
    locations: [],
    months: []
  });
  const [query, setQuery] = useState('');
  const [response, setResponse] = useState(null);
  const [oeeData, setOeeData] = useState(null);

  useEffect(() => {
    fetchFilters();
  }, []);

  const fetchFilters = async () => {
    try {
      const response = await axios.get('http://localhost:8000/api/filters');
      setAvailableFilters(response.data);
    } catch (error) {
      console.error('Error fetching filters:', error);
    }
  };

  const handleFileUpload = async (event) => {
    const file = event.target.files[0];
    if (!file) return;

    setLoading(true);
    const formData = new FormData();
    formData.append('file', file);

    try {
      await axios.post('http://localhost:8000/api/upload', formData);
      await fetchFilters();
      addMessage('File uploaded successfully. You can now query OEE data.', 'bot');
    } catch (error) {
      addMessage('Error uploading file. Please try again.', 'bot');
    } finally {
      setLoading(false);
    }
  };

  const addMessage = (text, sender, oeeData = null) => {
    setMessages(prev => [...prev, { text, sender, oeeData }]);
  };

  const handleSendMessage = async () => {
    if (!input.trim()) return;

    const userMessage = input;
    setMessages(prev => [...prev, { text: userMessage, sender: 'user' }]);
    setInput('');
    setLoading(true);

    try {
      const response = await axios.post('http://localhost:8000/api/query', {
        message: userMessage,
        ...filters
      });

      setMessages(prev => [...prev, {
        text: response.data.message,
        sender: 'bot',
        oeeData: {
          oee: response.data.oee,
          availability: response.data.availability,
          performance: response.data.performance,
          quality: response.data.quality
        }
      }]);
    } catch (error) {
      setMessages(prev => [...prev, {
        text: 'Sorry, I encountered an error processing your request.',
        sender: 'bot'
      }]);
    } finally {
      setLoading(false);
    }
  };

  const handleKeyPress = (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSendMessage();
    }
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      const res = await fetch('http://localhost:8000/query', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ query }),
      });
      const data = await res.json();
      setResponse(data.response);
      setOeeData(data.oee_data);
    } catch (error) {
      console.error('Error:', error);
      setResponse('Error processing query');
    }
  };

  return (
    <Container>
      <CssBaseline />
      <Box sx={{ mt: 4, mb: 4 }}>
        <Typography variant="h4" component="h1" gutterBottom>
          OEE Analysis Chat Interface
        </Typography>
        
        {/* Chat Messages */}
        <Paper elevation={3} sx={{ p: 2, mb: 2, maxHeight: '400px', overflow: 'auto' }}>
          <List>
            {messages.map((message, index) => (
              <ListItem key={index} sx={{ 
                justifyContent: message.sender === 'user' ? 'flex-end' : 'flex-start' 
              }}>
                <Paper elevation={1} sx={{ 
                  p: 1, 
                  bgcolor: message.sender === 'user' ? '#e3f2fd' : '#f5f5f5',
                  maxWidth: '80%'
                }}>
                  <ListItemText 
                    primary={message.text}
                    secondary={message.sender === 'user' ? 'You' : 'Assistant'}
                  />
                </Paper>
              </ListItem>
            ))}
          </List>
        </Paper>

        {/* Last OEE Data Dashboard */}
        {messages.length > 0 && messages[messages.length - 1].oeeData && (
          <OEEDashboard oeeData={messages[messages.length - 1].oeeData} />
        )}

        {/* Input Area */}
        <Box sx={{ display: 'flex', gap: 1, mt: 2 }}>
          <TextField
            fullWidth
            multiline
            maxRows={4}
            value={input}
            onChange={(e) => setInput(e.target.value)}
            onKeyPress={handleKeyPress}
            placeholder="Type your query here..."
            variant="outlined"
            disabled={loading}
          />
          <Button
            variant="contained"
            color="primary"
            onClick={handleSendMessage}
            disabled={loading || !input.trim()}
          >
            Send
          </Button>
        </Box>

        {response && (
          <Box sx={{ mt: 3 }}>
            <Typography variant="h6">Response:</Typography>
            <Typography paragraph>{response}</Typography>
          </Box>
        )}

        {oeeData && <OEEDashboard oeeData={oeeData} />}
      </Box>
    </Container>
  );
}

export default App; 