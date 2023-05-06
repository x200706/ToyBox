using System;
using System.Collections.Generic;
using System.Linq;
using System.Web;
using System.Web.Mvc;
using addressBook.Models;
using System.Web;
using System.Net;
using System.Data.Entity.Infrastructure;
using Microsoft.Ajax.Utilities;
using System.Reflection;

namespace addressBook.Controllers
{
    public class HomeController : Controller
    {
        StuffEntities db = new StuffEntities();


        public ActionResult Index()
        {
            var stuff = db.Table.OrderByDescending(x => x.Id).ToList();
            return View(stuff);
        }

        public ActionResult Create()
        {
            return View();
        }

        [HttpPost]
        [ValidateAntiForgeryToken]
        public ActionResult Create([Bind(Include="name,phone,email,site,remark,kind,birthday")]Table person)
        {
            if (ModelState.IsValid) {
            db.Table.Add(person);
            db.SaveChanges();
            return RedirectToAction("Index");
            }
            return View(person);
        }

        public ActionResult Edit(int? Id)
        {
            if (Id == null)
            {
                return new HttpStatusCodeResult(HttpStatusCode.BadRequest);
            }
            var person = db.Table.Find(Id);

            if (person == null)
            {
                return new HttpStatusCodeResult(HttpStatusCode.BadRequest);
            }
            return View(person);
        }

        [HttpPost]
        [ValidateAntiForgeryToken]
        public ActionResult Edit([Bind(Include = "Id,name,phone,email,site,remark,kind,birthday")] Table person)
        {
            if (ModelState.IsValid)
            {
                db.Entry(person).State=System.Data.Entity.EntityState.Modified;
                db.SaveChanges();
                return RedirectToAction("Index");
            }
            return View(person);
        }
            public ActionResult Details(int? Id)
        {
            if (Id == null) {
                return new HttpStatusCodeResult(HttpStatusCode.BadRequest);
            }
            var person = db.Table.Find(Id);

            if (person == null) {
                return new HttpStatusCodeResult(HttpStatusCode.BadRequest);
            }
            return View(person);
        }
        public ActionResult Delete(int Id)
        {
            var person = db.Table.Find(Id);
            db.Table.Remove(person);
            db.SaveChanges();
            return RedirectToAction("Index");
        }
    }
}