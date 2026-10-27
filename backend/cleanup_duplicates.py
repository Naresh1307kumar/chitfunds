import sys
import os
from sqlalchemy import func
from app.database import SessionLocal, engine
from app.models.plan_member import PlanMember
from app.models.chit_plan import ChitPlan
from app.models.installment import Installment
from app.models.draw import MonthlyDraw
from sqlalchemy import text

def cleanup_duplicates():
    db = SessionLocal()
    try:
        print("--- Finding duplicate plan memberships ---")
        duplicate_groups = (
            db.query(PlanMember.user_id, PlanMember.plan_id, func.count(PlanMember.id))
            .group_by(PlanMember.user_id, PlanMember.plan_id)
            .having(func.count(PlanMember.id) > 1)
            .all()
        )
        
        print(f"Found {len(duplicate_groups)} duplicate group(s).")
        
        for user_id, plan_id, count in duplicate_groups:
            members = (
                db.query(PlanMember)
                .filter(PlanMember.user_id == user_id, PlanMember.plan_id == plan_id)
                .order_by(PlanMember.is_active.desc(), PlanMember.id.asc())
                .all()
            )
            
            primary = members[0]
            duplicates = members[1:]
            
            print(f"User {user_id} in Plan {plan_id}: Keeping Primary ID {primary.id} (Ticket: {primary.ticket_number})")
            
            for dup in duplicates:
                print(f"  Removing Duplicate ID {dup.id} (Ticket: {dup.ticket_number})")
                
                # Reassign any installments if any exist
                installments = db.query(Installment).filter(Installment.plan_member_id == dup.id).all()
                for ins in installments:
                    ins.plan_member_id = primary.id
                    
                # Reassign any draws won if any exist
                draws = db.query(MonthlyDraw).filter(MonthlyDraw.winning_ticket_id == dup.id).all()
                for d in draws:
                    d.winning_ticket_id = primary.id
                    
                db.delete(dup)
                
        db.commit()
        
        # Update current_members count for all plans
        plans = db.query(ChitPlan).all()
        for plan in plans:
            actual_count = db.query(PlanMember).filter(PlanMember.plan_id == plan.id).count()
            if plan.current_members != actual_count:
                print(f"Updating Plan {plan.id} ({plan.plan_name}) current_members: {plan.current_members} -> {actual_count}")
                plan.current_members = actual_count
                
        db.commit()
        print("--- Cleanup complete! ---")
        
    except Exception as e:
        db.rollback()
        print("Error during cleanup:", e)
        raise
    finally:
        db.close()

if __name__ == "__main__":
    cleanup_duplicates()
