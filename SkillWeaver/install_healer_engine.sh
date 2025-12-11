#!/bin/bash

BASE="$HOME/Documents/skillweaver"

write() {
  FILE="$1"
  CONTENT="$2"
  echo "$CONTENT" | base64 --decode > "$FILE"
}

##############################################################
# 1. PriorityProfiles.lua
##############################################################
write "$BASE/healer/PriorityProfiles.lua" "
bG9jYWwgcHJvZmlsZXMgPSB7CgogICAgU2FmZXR5ID0gewogICAgICAgICJlbWVyZ2VuY3kiLCAiY2xlYW5zZSIsICJzZWxmIiwgInRhbmsiLAogICAgICAgICJhb2UiLCAiY29vbGRvd24iLCAiZmFzdCIsICJlZmZpY2llbnQiLCAiZHBzIgogICAgfSwKCiAgICBBZ2dyZXNzaXZlID0gewogICAgICAgICJjb29sZG93biIsICJhb2UiLCAiZmFzdCIsICJ0YW5rIiwKICAgICAgICAic2VsZiIsICJlbWVyZ2VuY3kiLCAiZWZmaWNpZW50IiwgImNsZWFuc2UiLCAiZHBzIgogICAgfSwKCiAgICBUYW5rSGVhbGVyID0gewogICAgICAgICJ0YW5rIiwgImVtZXJnZW5jeSIsICJzZWxmIiwgImNvb2xkb3duIiwKICAgICAgICAiYW9lIiwgImNsZWFuc2UiLCAiZmFzdCIsICJlZmZpY2llbnQiLCAiZHBzIgogICAgfSwKCiAgICBSYWlkSGVhbGVyID0gewogICAgICAgICJhb2UiLCAiY29vbGRvd24iLCAiZmFzdCIsICJlZmZpY2llbnQiLAogICAgICAgICJjbGVhbnNlIiwgInRhbmsiLCAic2VsZiIsICJlbWVyZ2VuY3kiLCAiZHBzIgogICAgfSwKCiAgICBIeWJyaWQgPSB7CiAgICAgICAgImVtZXJnZW5jeSIsICJjbGVhbnNlIiwgInRhbmsiLCAic2VsZiIsCiAgICAgICAgImFvZSIsICJjb29sZG93biIsICJmYXN0IiwgImVmZmljaWVudCIsICJkcHMiCiAgICB9LAoKICAgIEN1c3RvbSA9IHt9Cn0KCnJldHVybiBwcm9maWxlcwo=
"

##############################################################
# 2. HealerUltra.lua
##############################################################
write "$BASE/healer/HealerUltra.lua" "
bG9jYWwgcHJvZmlsZXMgPSByZXF1aXJlKCJza2lsbHdldmVyLmhlYWxlci5Qcmlvcml0eVByb2ZpbGVzIikKCmxvY2FsIFUgPSB7fQoKVS5jdXJyZW50UHJvZmlsZSA9ICJIeWJyaWQiClUuY3VzdG9tUHJvZmlsZSA9IHt9CgpmdW5jdGlvbiBVOlNldFByb2ZpbGUobmFtZSkKICAgIGlmIG5hbWUgPT0gIkN1c3RvbSIgdGhlbgogICAgICAgIFNlZlUuY3VycmVudFByb2ZpbGUgPSAiQ3VzdG9tIgogICAgZWxzZQogICAgICAgIFUuY3VycmVudFByb2ZpbGUgPSBwcm9maWxlc1tuYW1lXSBhbmQgbmFtZSBvciAiSHlicmlkIgogICAgZW5kCmVuZAoKZnVuY3Rpb24gVToiR2V0UHJpb3JpdHlMaXN0IiAoKQogICAgaWYgVS5jdXJyZW50UHJvZmlsZSA9PSAiQ3VzdG9tIiB0aGVuCiAgICAgICAgcmV0dXJuIFUuY3VzdG9tUHJvZmlsZQogICAgZWxzZQogICAgICAgIHJldHVybiBwcm9maWxlc1tVLmN1cnJlbnRQcm9maWxlXQogICAgZW5kCmVuZAoKZnVuY3Rpb24gVToiR2V0UmVjb21tZW5kZWRTcGVsbCIgKGNvbnRleHQpCiAgICBsb2NhbCBwID0gVToiR2V0UHJpb3JpdHlMaXN0IiAoKQogICAgZm9yIF8sIGtleSBpbiBwIGRvCiAgICAgICAgaWYgY29udGV4dFtrZXldIGFuZCBjb250ZXh0W2tleV0udXNhYmxlIHRoZW4KICAgICAgICAgICAgcmV0dXJuIGNvbnRleHRba2V5XS5zcGVsbCwga2V5CiAgICAgICAgZW5kCiAgICBlbmQKICAgIHJldHVybiBuaWwsIG5pbApjbmQKCnJldHVybiBVCg==
"

##############################################################
# 3. HealSnap.lua
##############################################################
write "$BASE/healer/HealSnap.lua" "
bG9jYWwgUyA9IHt9CgpTLmN1cnJlbnRUYXJnZXQgPSBuaWxsClMuc25hcEFjdGl2ZSA9IGZhbHNlCgpmdW5jdGlvbiBTOkJlZ2luU25hcChyZWNvbW1lbmRlZFRhcmdldCkKICAgIFMuc25hcEFjdGl2ZSA9IHRydWUKICAgIFMuY3VycmVudFRhcmdldCA9IHJlY29tbWVuZGVkVGFyZ2V0CmVuZAoKZnVuY3Rpb24gUzpVcGRhdGVUYXJnZXRGcm9tU3RpY2soZGlyZWN0aW9uLCBjYW5kaWRhdGVzKQogICAgaWYgbm90IFMuc25hcEFjdGl2ZSB0aGVuIHJldHVybiBlbmQKICAgIGxvY2FsIGlkeCA9IDEKICAgIGZvciBpLCB0IGluIGlwaWNvaXMgY2FuZGlkYXRlcyBkbwogICAgICAgIGlmIHQgPT0gUy5jdXJyZW50VGFyZ2V0IHRoZW4gaWR4ID0gaSBlbmQKICAgIGVuZAogICAgbG9jYWwgbmV4dCA9IGRpcmVjdGlvbiA9PSAibGVmdCIgYW5kIGlkeCAtIDEgb3IgaWR4ICsgMQogICAgaWYgY2FuZGlkYXRlc1tuZXh0XSB0aGVuCiAgICAgICAgUy5jdXJyZW50VGFyZ2V0ID0gY2FuZGlkYXRlc1tuZXh0XQogICAgZW5kCmVuZAoKZnVuY3Rpb24gUzpFbmRTbmFwKCkKICAgIFMuc25hcEFjdGl2ZSA9IGZhbHNlCiAgICByZXR1cm4gUy5jdXJyZW50VGFyZ2V0CmVuZAoKcmV0dXJuIFMK
"

##############################################################
# 4. HealerUI.lua
##############################################################
write "$BASE/healer/HealerUI.lua" "
bG9jYWwgVUk9IHt9CgpVSS5jdXJyZW50U3BlbGwgPSBuaWxsClVJLnJlYXNvbiA9IG5pbGwKCmZ1bmN0aW9uIFVJOlNob3dSZWNvbW1lbmRhdGlvbihzcGVsbCwgcmVhc29uLCB0YXJnZXQpCiAgICBWS
XS5jdXJyZW50U3BlbGwgPSBzcGVsbAogICAgVUkucmVhc29uID0gcmVhc29uCiAgICBwcmludCgiW1NraWxsV2VhdmVyXSBIZWFsZXIgVVJleyIgLiBzcGVsbCAuICIgIiAuIHJlYXNvbiAuICIpIC4gIiDigKIgVGF
yZ2V0OiAiIC4gKHRhcmdldCBvciAiPz8/IikpCmVuZAoKcmV0dXJuIFVJCg==
"

##############################################################
# 5. HealerBindings.lua
##############################################################
write "$BASE/healer/HealerBindings.lua" "
bG9jYWwgQiA9IHt9CgpCLmlucHV0TW9kZSA9ICJrZXlib2FyZCIKCmZ1bmN0aW9uIEI6U2V0TW9kZShtb2RlKQogICAgQi5pbnB1dE1vZGUgPSBtb2RlCmVuZAoKZnVuY3Rpb24gQjpPbk1haW5CdXR0b25QcmVzc2VkKGNhc3RGdW5jKQogICAgY2FzdEZ1bmMoKQplbmQKCnJldHVybiBCCg==
"

##############################################################
# 6. Healer Configs — full set
##############################################################

# Holy Paladin
write "$BASE/healer_configs/paladin_holy.lua" "
cmV0dXJuIHsKICAgIGZhc3QgPSAiRmxhc2ggb2YgTGlnaHQiLAogICAgZWZmaWNpZW50ID0gIkhvbHkgTGlnaHQiLAogICAgZW1lcmdlbmN5ID0gIkxh
eSBvbiBIYW5kcyIsCiAgICB0YW5rID0gIldvcmQgb2YgR2xvcnkiLAogICAgYW9lID0gIkRheWJyZWFrIiwKICAgIGNsZWFuc2UgPSAiQ2xlYW5zZSIsCn0K
"

# Holy Priest
write "$BASE/healer_configs/priest_holy.lua" "
cmV0dXJuIHsKICAgIGZhc3QgPSAiRmxhc2ggSGVhbCIsCiAgICBlZmZpY2llbnQgPSAiSGVhbCIsCiAgICBlbWVyZ2VuY3kgPSAiRGVzcGVyYXRlIFByYXllciIsCiAgICB0YW5rID0gIkd1YXJkaWFuIFNwaXJpdCIsCiAgICBhb2UgPSAiUHJheWVyIG9mIEhlYWxpbmciLAogICAgY2xlYW5zZSA9ICJQdXJpZnkiLAp9Cg==
"

# Discipline Priest
write "$BASE/healer_configs/priest_disc.lua" "
cmV0dXJuIHsKICAgIGZhc3QgPSAiRmxhc2ggSGVhbCIsCiAgICBlZmZpY2llbnQgPSAiSGVhbCIsCiAgICBlbWVyZ2VuY3kgPSAiUGFpbiBTdXBwcmVzc2lvbiIsCiAgICB0YW5rID0gIlBvd2VyIFdvcmQ6IFNoaWVsZCIsCiAgICBhb2UgPSAiUGVuYW5jZSIsCiAgICBjbGVhbnNlID0gIlB1cmlmeSIsCn0K
"

# Resto Druid
write "$BASE/healer_configs/druid_resto.lua" "
cmV0dXJuIHsKICAgIGZhc3QgPSAiUmVncm93dGgiLAogICAgZWZmaWNpZW50ID0gIlJlanV2ZW5hdGlvbiIsCiAgICBlbWVyZ2VuY3kgPSAiSXJvbmJhcmsiLAogICAgdGFuayA9ICJMaWZlYmxvb20iLAogICAgYW9lID0gIldpbGQgR3Jvd3RoIiwKICAgIGNsZWFuc2UgPSAiTmF0dXJlJ3MgQ3VyZSIsCn0K
"

# Resto Shaman
write "$BASE/healer_configs/shaman_resto.lua" "
cmV0dXJuIHsKICAgIGZhc3QgPSAiSGVhbGluZyBTdXJnZSIsCiAgICBlZmZpY2llbnQgPSAiSGVhbGluZyBXYXZlIiwKICAgIGVtZXJnZW5jeSA9ICJTcGlyaXQgTGluayBUb3RlbSIsCiAgICB0YW5rID0gIlJpcHRpZGUiLAogICAgYW9lID0gIkNoYWluIEhlYWwiLAogICAgY2xlYW5zZSA9ICJQdXJpZnkgU3BpcnQiLAogIH0K
"

# Mistweaver Monk
write "$BASE/healer_configs/monk_mw.lua" "
cmV0dXJuIHsKICAgIGZhc3QgPSAiVml2aWZ5IiwKICAgIGVmZmljaWVudCA9ICJTb290aGluZyBNaXN0IiwKICAgIGVtZXJnZW5jeSA9ICJMaWZlIENvY29vbiIsCiAgICB0YW5rID0gIkVudmVsb3BpbmcgTWlzdCIsCiAgICBhb2UgPSAiUmVmcmVzaGluZyBKYWRlIFdpbmQiLAogICAgY2xlYW5zZSA9ICJEZXRveCIsCn0K
"

# Preservation Evoker
write "$BASE/healer_configs/evoker_preservation.lua" "
cmV0dXJuIHsKICAgIGZhc3QgPSAiTGl2aW5nIEZsYW1lIiwKICAgIGVmZmljaWVudCA9ICJFbWVy
YWxkIEJsb3Nzb20iLAogICAgZW1lcmdlbmN5ID0gIlJld2luZCIsCiAgICB0YW5rID0gIkVjaG8iLAogICAgYW9lID0gIkRyZWFtIEJyZWF0aCIsCiAgICBjbGVhbnNlID0gIkV4cHVuZ2UiLAogIH0K
"

echo "Healer Engine Installed Successfully!"
