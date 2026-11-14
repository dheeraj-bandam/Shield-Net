# Shield-Net: Supply and Demand Matching Prototype

A Streamlit prototype that demonstrates how face-shield suppliers can be matched with healthcare requesters. It supports sample scenarios and editable inputs, then presents suggested allocations, estimated distance, unmet demand, supplier utilization, and a descriptive recommendation.

## Run locally

```bash
python -m pip install -r requirements.txt
streamlit run shield_net_app.py
```

## Notes

This is a demonstration prototype using sample data and a heuristic allocation approach. It does not reproduce the historical Shield-Net optimization model or independently verify its reported results. Distances are estimates based on the sample coordinates. The app does not contact suppliers or place orders.

## Deploy on Streamlit Community Cloud

1. Push this repository to GitHub.
2. In Streamlit Community Cloud, create an app from the repository.
3. Set the main file path to `shield_net_app.py` and deploy.
