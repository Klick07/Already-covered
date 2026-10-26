# Demo video script v2 (target 4:45, hard limit 5:00)

Required by the rules: the team, the app working, the architecture, the principal results, public or unlisted link. Everything below says "recorded footage" where it is, because nothing was live. Narration at about 140 words/min (about 660 words total).

**Before recording**
- Server up, dashboard URL open (it shows the saved Room 1 run, a *replay*). The quick-tunnel URL changes after restarts, so open it fresh and keep the tunnel running while recording.
- Tabs: dashboard, `architecture_v2.png`, `merge_vicon_room1.png`, the Section 11 table of the report, and (when it exists) the final-footage result.
- Do **not** press Approve or Reject on replay approval cards. They are replay-generated.
- Restart the replay right before shot 4 (`~/replay_v1.sh`, about 290 s, rules only), so the events appear on screen.

## 1. Team and problem (0:00-0:30)
**Screen:** team on camera or a title card with names. [TEAM: names]
> We're [team]. People who map a building with cameras film the same area twice, miss that their footage went bad, and trust maps built from wrong matches. We built a system where three stereo cameras map together, and a coordinator tells each walker what to do next, but asks a person when the visual evidence is weak.

## 2. Architecture (0:30-1:10)
**Screen:** `architecture_v2.png`, cursor along the flow.
> Each stereo pair goes through our OpenCV 5 front end: rectify, then score for blur, ORB features, and tracking. Swarm-SLAM on one AWS EC2 server merges three robots' maps. A recorder turns it into events. The coordinator re-checks every proposed overlap with OpenCV 5, and the guardrail that blocks weak overlaps is in code. In the first phase the coordinator used Amazon Nova on Bedrock. The later runs used the same rules in code, no model. All input is recorded footage. We have no live capture.

## 3. OpenCV 5 doing real work (1:10-1:35)
**Screen:** dashboard camera tiles with their scores.
> These are rectified frames from three recorded EuRoC flights. On raw pairs, zero percent of left-right matches line up on the same row. After our OpenCV 5 rectification it's ninety percent. Under each camera: tracking score and feature count against the warning thresholds.

## 4. The coordinator acting (1:35-2:40)
**Screen:** dashboard, replay running. Wait for an "Area covered" row, then an approval card. Do not click it.
> This is a replay of a saved Room 1 run, running our rules at three times the original pace. Cameras 0 and 2 see the same checkerboard. OpenCV 5 finds 138 consistent matches [check these numbers on screen against the replay before recording] spread across both images, so the area is marked covered and camera 2 is told to move on.
> Now a tricky one: 248 matches, packed onto the checkerboard. A repetitive pattern can fool a matcher, so coverage is put on hold and a person is asked. The card shows both keyframes with the matches. In the original run a person answered these cards, and the log credits them. In this replay nobody has decided, and we don't press the buttons.

**Screen:** scroll the decision log.
> Every row records the OpenCV and Swarm-SLAM values, who decided, and how long it took.

## 5. EuRoC results, checked against ground truth (2:40-3:25)
**Screen:** `merge_vicon_room1.png`, then the results table.
> On EuRoC, with motion-capture ground truth: unmerged, the three room maps are 90 centimetres off. Merged, one alignment puts them within 21 centimetres. In the industrial hall it's 8 to 9 centimetres. Every "area covered" claim we could check was correct. In the room the system found two thirds of the shared places.

## 6. New footage: AirMuseum, with honest limits (3:25-4:05)
**Screen:** the AirMuseum cloud (if that saved run can be opened on the dashboard; otherwise a screenshot of it), then the Section 11 table.
> We also ran uploaded AirMuseum footage: a hangar, three robots at 10 frames a second. At quarter speed we built a cloud of about 595 thousand points. Fed at real speed on this two-core server, the stored map ran about a minute behind, and full tracking kept only about 60 percent of frames. So real-time is not demonstrated. And without verified ground truth there, our three-to-four-metre error figure is not an accuracy claim.

## 7. Failure cases (4:05-4:35)
**Screen:** `perturb_blank.jpg`, `perturb_shake.jpg`, the failure table.
> We injected a blank wall and a quick shake: warnings within a third of a second. Our blur threshold failed in a darker room, 52 false warnings, so we switched to tracking quality. The first time, SLAM never recovered and the agent said "tracking OK"; we fixed both. Of six planted look-alike closures, four went to a human and two slipped through, and we report that.

## 8. Final footage and close (4:35-4:55)
**Screen:** the final-footage result, or a title card. [PENDING: only say what was measured]
> Finally, our own stereo recordings: [PENDING result in one honest sentence]. Code, report and results are in the repository. Thanks for watching.

**Checklist:** under 5:00, team shown, app working (shots 3-4), architecture (shot 2), principal results (5-6), limitations (6-7), upload public or unlisted, put the link in the submission.
