export interface CommandApiBlocker {
  blocker_id: string;
  type: string;
  stage: string;
  reason: string;
  source_ref: string;
  next_action: string;
}
