
⸻

Classroom Lab Connection Instructions

Welcome to the lab environment 👋
Follow the steps below to connect to your pod and start working.

⸻

1. Connect to the jump server

From your terminal or SSH client, run:

ssh jump@PROVIDED_BY_INSTRUCTOR

Password:

800-ePlus


⸻

2. Connect to your assigned pod

Once you’re logged in to the jump server, connect to your pod.

Examples:

ssh pod1@jump
ssh pod7@jump
ssh pod12@jump

Password for all pods:

800-ePlus

✅ Use the pod number you’ve been assigned (PodXX), for example pod3.

⸻

3. Lab materials

All lab files and instructions are available here:

🔗 Labs Repository: https://github.com/actswartz/dlr

⸻

Using SSH from Windows or Mac

You’ll use an SSH client to connect to the lab.

SSH (Secure Shell) is a secure way to open a command-line session on a remote system.

⸻

macOS (Mac) Users

Macs already have SSH built in.
	1.	Open Terminal
	•	Press Command + Space, type Terminal, and press Enter.
	2.	At the prompt, run:

ssh jump@PROVIDED_BY_INSTRUCTOR


	3.	When asked:
Are you sure you want to continue connecting (yes/no)?

Type:

yes

and press Enter (you only see this the first time).

	4.	Enter the password:

800-ePlus


	5.	Once you’re on the jump server, connect to your pod:

ssh podXX@jump

Replace XX with your pod number (for example, pod3).

⸻

Windows Users

You have a few options. Any of these is fine.

Option A – Built-in SSH (Windows 10/11)
	1.	Open Windows Terminal, PowerShell, or Command Prompt:
	•	Press the Windows key, type PowerShell or Windows Terminal, and press Enter.
	2.	Run:

ssh jump@PROVIDED_BY_INSTRUCTOR


	3.	If you see a message about the host key and:
Are you sure you want to continue connecting (yes/no)?

Type:

yes

and press Enter.

	4.	Enter the password:

800-ePlus


	5.	Then connect to your pod:

ssh podXX@jump

Replace XX with your assigned pod number.

⸻

Option B – Using a GUI SSH Client (PuTTY, Termius, etc.)

If you prefer a graphical tool, you can use:
	•	PuTTY – Free, classic Windows SSH client
	•	Termius – Available on Windows, Mac, Linux, iOS, Android

Example with PuTTY
	1.	Download and install PuTTY.
	2.	Open PuTTY.
	3.	In Host Name (or IP address), enter:

PROVIDED_BY_INSTRUCTOR


	4.	Click Open.
	5.	When the terminal window appears, log in:
	•	Username: jump
	•	Password: 800-ePlus
	6.	Once on the jump server, type:

ssh podXX@jump

and use the same password:

800-ePlus



⸻

Tips & Troubleshooting
	•	Copy/Paste:
	•	Mac Terminal: copy normally, paste with Command + V.
	•	Windows PowerShell/Terminal: copy normally, paste with Ctrl + V.
	•	Common issues:
	•	If you get “Permission denied” or “Connection closed”, double-check:
	•	Username (jump, pod1, pod2, etc.)
	•	Address (PROVIDED_BY_INSTRUCTOR from your instructor)
	•	Password (800-ePlus)

If you still can’t connect, take a screenshot or copy the error message and let your instructor know.
