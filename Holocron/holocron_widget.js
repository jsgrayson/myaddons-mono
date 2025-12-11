// Holocron Widget for Scriptable (iOS)
// Copy this into the Scriptable App

const SERVER_URL = "http://localhost:5001"; // Update this!

let widget = await createWidget();
if (config.runsInWidget) {
    Script.setWidget(widget);
} else {
    widget.presentMedium();
}
Script.complete();

async function createWidget() {
    let w = new ListWidget();
    w.backgroundColor = new Color("#1a1a1a");

    // Title
    let title = w.addText("Holocron Command");
    title.textColor = new Color("#0070dd");
    title.font = Font.boldSystemFont(16);
    w.addSpacer(8);

    try {
        // Fetch Data (Mocking the endpoint for now)
        // let req = new Request(`${SERVER_URL}/api/dashboard/summary`);
        // let data = await req.loadJSON();

        // Mock Data
        let data = {
            gold: "1,240,500g",
            next_event: "Raid: ICC (20:00)",
            alerts: 2
        };

        // Gold
        let goldLine = w.addText(`💰 ${data.gold}`);
        goldLine.textColor = Color.white();
        goldLine.font = Font.systemFont(14);

        // Event
        let eventLine = w.addText(`📅 ${data.next_event}`);
        eventLine.textColor = Color.white();
        eventLine.font = Font.systemFont(14);

        // Alerts
        if (data.alerts > 0) {
            w.addSpacer(4);
            let alertLine = w.addText(`🚨 ${data.alerts} Active Alerts`);
            alertLine.textColor = new Color("#ff4444");
            alertLine.font = Font.boldSystemFont(12);
        }

    } catch (e) {
        let err = w.addText("Connection Failed");
        err.textColor = Color.red();
    }

    return w;
}
