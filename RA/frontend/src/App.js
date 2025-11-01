import React, { useState, useEffect } from 'react';
import axios from 'axios';

function App() {
  const [bid, setBid] = useState("");
  const [message, setMessage] = useState("");
  const [socket, setSocket] = useState(null);

  useEffect(() => {
    const ws = new WebSocket("ws://127.0.0.1:8000/ws/1");
    ws.onmessage = (msg) => setMessage(msg.data);
    setSocket(ws);
    return () => ws.close();
  }, []);

  const sendBid = async () => {
    await axios.post("http://127.0.0.1:8000/bid", {
      auction_id: 1,
      user_id: 101,
      bid_amount: parseFloat(bid)
    });
    if (socket) socket.send(`Bid placed: ${bid}`);
    setBid("");
  };

  return (
    <div style={{ textAlign: 'center', marginTop: 40 }}>
      <h1>Reverse Auction</h1>
      <input value={bid} onChange={e => setBid(e.target.value)} placeholder="Enter your bid" />
      <button onClick={sendBid}>Submit Bid</button>
      <p>{message}</p>
    </div>
  );
}

export default App;
